from rest_framework import serializers as ser
from framework.auth.core import Auth
from website.project.model import Comment
from rest_framework.exceptions import ValidationError, PermissionDenied
from api.base.exceptions import InvalidModelValueError
from api.base.utils import absolute_reverse
from api.base.settings import osf_settings
from api.base.serializers import (JSONAPISerializer,
                                  TargetField,
                                  RelationshipField,
                                  IDField, TypeField, LinksField,
                                  AuthorizedCharField)


class CommentReport(object):
    def __init__(self, user_id, category, text):
        self._id = user_id
        self.category = category
        self.text = text


class CommentSerializer(JSONAPISerializer):

    filterable_fields = frozenset([
        'deleted',
        'date_created',
        'date_modified'
    ])

    id = IDField(source='_id', read_only=True)
    type = TypeField()
    content = AuthorizedCharField(source='get_content', max_length=osf_settings.COMMENT_MAXLENGTH)

    target = TargetField(link_type='related', meta={'type': 'get_target_type'})
    user = RelationshipField(related_view='users:user-detail', related_view_kwargs={'user_id': '<user._id>'})
    node = RelationshipField(related_view='nodes:node-detail', related_view_kwargs={'node_id': '<node._id>'})
    replies = RelationshipField(self_view='comments:comment-replies', self_view_kwargs={'comment_id': '<pk>'})
    reports = RelationshipField(related_view='comments:comment-reports', related_view_kwargs={'comment_id': '<pk>'})

    date_created = ser.DateTimeField(read_only=True)
    date_modified = ser.DateTimeField(read_only=True)
    modified = ser.BooleanField(read_only=True, default=False)
    deleted = ser.BooleanField(read_only=True, source='is_deleted', default=False)
    is_abuse = ser.SerializerMethodField()
    has_children = ser.SerializerMethodField()
    can_edit = ser.SerializerMethodField()

    # LinksField.to_representation adds link to "self"
    links = LinksField({})

    class Meta:
        type_ = 'comments'

    def get_is_abuse(self, obj):
        auth = Auth(self.context['request'].user)
        if not auth or auth.user.is_anonymous():
            return False
        return auth.user and auth.user._id in obj.reports

    def get_can_edit(self, obj):
        auth = Auth(self.context['request'].user)
        if not auth or auth.user.is_anonymous():
            return False
        return obj.user._id == auth.user._id

    def get_has_children(self, obj):
        return bool(getattr(obj, 'commented', []))

    def create(self, validated_data):
        user = validated_data['user']
        auth = Auth(user)
        node = validated_data['node']

        content = validated_data.pop('get_content')
        validated_data['content'] = content.strip()
        if not validated_data['content']:
            raise ValidationError('Comment cannot be empty.')

        if node and node.can_comment(auth):
            comment = Comment.create(auth=auth, **validated_data)
        else:
            raise PermissionDenied("Not authorized to comment on this project.")
        return comment

    def update(self, comment, validated_data):
        assert isinstance(comment, Comment), 'comment must be a Comment'
        auth = Auth(self.context['request'].user)
        if validated_data:
            if 'get_content' in validated_data:
                content = validated_data.pop('get_content')
                content = content.strip()
                if not content:
                    raise ValidationError('Comment cannot be empty.')
                comment.edit(content, auth=auth, save=True)
            if validated_data.get('is_deleted', None) is True:
                comment.delete(auth, save=True)
            elif comment.is_deleted:
                comment.undelete(auth, save=True)
        return comment

    def get_target_type(self, obj):
        object_type = obj._name
        if not object_type or object_type not in ['comment', 'node']:
            raise InvalidModelValueError('Invalid comment target.')
        return object_type


class CommentDetailSerializer(CommentSerializer):
    """
    Overrides CommentSerializer to make id required.
    """
    id = IDField(source='_id', required=True)
    deleted = ser.BooleanField(source='is_deleted', required=True)


class CommentReportSerializer(JSONAPISerializer):
    id = IDField(source='_id', read_only=True)
    type = TypeField()
    category = ser.ChoiceField(choices=[('spam', 'Spam or advertising'),
                                        ('hate', 'Hate speech'),
                                        ('violence', 'Violence or harmful behavior')], required=True)
    message = ser.CharField(source='text', required=False, allow_blank=True)
    links = LinksField({'self': 'get_absolute_url'})

    class Meta:
        type_ = 'comment_reports'

    def get_absolute_url(self, obj):
        comment_id = self.context['request'].parser_context['kwargs']['comment_id']
        return absolute_reverse(
            'comments:report-detail',
            kwargs={
                'comment_id': comment_id,
                'user_id': obj._id
            }
        )

    def create(self, validated_data):
        user = self.context['request'].user
        comment = self.context['view'].get_comment()
        if user._id in comment.reports:
            raise ValidationError('Comment already reported.')
        try:
            comment.report_abuse(user, save=True, **validated_data)
        except ValueError:
            raise ValidationError('You cannot report your own comment.')
        return CommentReport(user._id, **validated_data)

    def update(self, comment_report, validated_data):
        user = self.context['request'].user
        comment = self.context['view'].get_comment()
        if user._id != comment_report._id:
            raise ValidationError('You cannot report a comment on behalf of another user.')
        try:
            comment.report_abuse(user, save=True, **validated_data)
        except ValueError:
            raise ValidationError('You cannot report your own comment.')
        return CommentReport(user._id, **validated_data)


class CommentReportDetailSerializer(CommentReportSerializer):
    """
    Overrides CommentReportSerializer to make id required.
    """
    id = IDField(source='_id', required=True)
