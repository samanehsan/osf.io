from os.path import basename

from website import settings


def serialize_addon_config(config, user, node=None):
    lookup = config.template_lookup

    user_addon = user.get_addon(config.short_name)
    node_addon = node.get_addon(config.short_name) if node else None

    ret = {
        'addon_short_name': config.short_name,
        'addon_full_name': config.full_name,
        'category': config.categories[0],
        'is_enabled': user_addon is not None,
        'is_configured': node_addon and node_addon.has_auth,
        'addon_icon_url': config.icon_url,
    }
    if not node:
        ret.update({
            'user_settings_template': lookup.get_template(basename(config.user_settings_template)),
        })
    ret.update(node_addon.to_json(user) if node and node_addon else {})
    ret.update(user_addon.to_json(user) if user_addon else {})
    return ret


def get_addons_by_config_type(config_type, user, node=None):
    addons = [addon for addon in settings.ADDONS_AVAILABLE if config_type in addon.owners and addon.short_name != 'osfstorage']
    return [serialize_addon_config(addon_config, user, node) for addon_config in sorted(addons, key=lambda cfg: cfg.full_name.lower())]
