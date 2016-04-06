var Comment = require('js/comment'); //jshint ignore:line
var ctx = window.contextVars;

var currentUser = {
    id: ctx.currentUser.id,
    url: ctx.currentUser.urls.profile,
    fullname: ctx.currentUser.fullname,
    gravatarUrl: ctx.currentUser.gravatarUrl
};
var options = {
    nodeId : window.contextVars.node.id,
    nodeApiUrl: window.contextVars.node.urls.api,
    isRegistration: window.contextVars.node.isRegistration,
    page: 'total',
    rootId: null,
    fileId: null,
    commentId: window.contextVars.comment.id,
    canComment: window.contextVars.currentUser.canComment,
    hasChildren: window.contextVars.node.hasChildren,
    currentUser: currentUser
};
Comment.init('#commentsLink', '#discussions', options);
