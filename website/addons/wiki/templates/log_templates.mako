<script type="text/html" id="wiki_updated">
updated wiki page
<a data-bind="attr: {href: wikiUrl}, text: params.page"></a>
to version <span data-bind="text: params.version"></span>
of <a class = "log-node-title-link overflow" data-bind="text:nodeTitle, attr: {href: nodeUrl}"></a>
</script>

<script type="text/html" id="wiki_renamed">
renamed wiki page
<a data-bind="attr: {href: wikiIdUrl}, text: params.old_page"></a>
to <a data-bind="attr: {href: wikiIdUrl}, text: params.page"></a>
of <a class = "log-node-title-link overflow" data-bind="text:nodeTitle, attr: {href: nodeUrl}"></a>
</script>

<script type="text/html" id="wiki_deleted">
deleted wiki page
<a data-bind="attr: {href: wikiUrl}, text: params.page"></a>
of <a class = "log-node-title-link overflow" data-bind="text:nodeTitle, attr: {href: nodeUrl}"></a>
</script>
