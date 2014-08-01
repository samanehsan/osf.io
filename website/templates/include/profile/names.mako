<script id="profileName" type="text/html">

    <form role="form" data-bind="submit: submit">

        <div class="form-group">
            <label>Account email address:</label>
            <input class="form-control" data-bind="value: username" />
        </div>

        <div class="form-group">
            <label>Full Name (e.g. Rosalind Elsie Franklin)</label>
            <input class="form-control" data-bind="value: full" />
        </div>

        <span class="help-block">
            Your full name, above, is the name that will be displayed in your profile.
            To control the way your name will appear in citations, you can use the
            "Guess names" button to automatically infer your first name, last
            name, etc., or edit the fields directly below.
        </span>

        <div style="margin-bottom: 10px;">
            <a class="btn btn-default" data-bind="enabled: hasFirst(), click: impute">Guess names</a>
        </div>

        <div class="form-group">
            <label>Given Name (e.g. Rosalind)</label>
            <input class="form-control" data-bind="value: given" />
        </div>

        <div class="form-group">
            <label>Middle Name(s) (e.g. Elsie)</label>
            <input class="form-control" data-bind="value: middle" />
        </div>

        <div class="form-group">
            <label>Family Name (e.g. Franklin)</label>
            <input class="form-control" data-bind="value: family" />
        </div>

        <div class="form-group">
            <label>Suffix</label>
            <input class="form-control" data-bind="value: suffix" />
        </div>

        <hr />

        <h4>Citation Preview</h4>

        <table class="table">
            <thead>
                <tr>
                    <th>Style</th>
                    <th>Citation Format</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>APA</td>
                    <td>{{ citeApa }}</td>
                </tr>
                <tr>
                    <td>MLA</td>
                    <td>{{ citeMla }}</td>
                </tr>
            </tbody>
        </table>

        <div class="padded">

            <button
                    type="submit"
                    class="btn btn-default"
                    data-bind="visible: viewable, click: cancel"
                >Cancel</button>

            <button
                    type="submit"
                    class="btn btn-primary"
                    data-bind="enable: enableSubmit"
                >Submit</button>

        </div>

        <!-- Flashed Messages -->
        <div class="help-block">
            <p data-bind="html: message, attr.class: messageClass"></p>
        </div>

    </form>

</script>
