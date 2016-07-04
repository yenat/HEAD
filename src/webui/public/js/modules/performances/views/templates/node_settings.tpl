<div class="app-node-content">
    <div data-node-property="animation" class="app-gesture-select"></div>
    <div data-node-property="emotion" class="app-emotion-list"></div>
    <div data-node-property="expression" class="app-expression-list"></div>
</div>

<div class="app-options-content">
    <div class="app-node-properties col-sm-12">
        <div class="form-group">
            <label>Start time</label>

            <div class="input-group">
                <input type="text" class="app-node-start-time form-control" title="Start time"/>

                <div class="input-group-addon">s</div>
            </div>
        </div>

        <div class="form-group" data-node-property="duration">
            <label>Duration</label>

            <div class="input-group">
                <input type="text" class="app-node-duration form-control" title="Duration"/>

                <div class="input-group-addon">s</div>
            </div>
        </div>

        <div class="form-group" data-node-property="message">
            <label>Message</label>

            <div class="input-group">
                <input type="text" class="app-node-message-input form-control" title="Message"/>
            </div>
        </div>

        <div class="form-group" data-node-property="speed">
            <label>Speed <span class="app-speed-label pull-right label label-default"></span></label>

            <div class="app-speed-slider"></div>
        </div>

        <div class="form-group" data-node-property="angle">
            <label>Angle <span class="app-hr-angle-label pull-right label label-default"></span></label>
            <div class="app-hr-angle-slider"></div>
        </div>

        <div class="form-group" data-node-property="btree_mode">
            <label title="Mode">Mode</label>
            <select class="app-btree-mode-select">
                <option value="255">Full</option>
                <option value="207">FT Off</option>
                <option value="48">FT On</option>
            </select>
        </div>

        <div class="form-group" data-node-property="speech_event">
            <label title="Language">Speech event</label>
            <select class="app-speech-event-select">
                <option value="">None</option>
                <option value="listening">Listening</option>
                <option value="talking">Talking</option>
            </select>
        </div>

        <div class="form-group" data-node-property="kfanimation">
            <label title="Animation">Animation</label>
            <select class="app-kfanimation-select"></select>
        </div>

        <div class="form-group" data-node-property="fps">
            <label title="FPS">FPS <span
                        class="app-fps-label pull-right label label-default"></span></label>
            <div class="app-fps-slider"></div>
        </div>

        <div class="form-group" data-node-property="kfmode">
            <label title="Arms">Blender Disabled</label>
            <select class="app-kfmode-select">
                <option value="no">No</option>
                <option value="face">Face</option>
                <option value="all">All</option>
            </select>
        </div>

        <div class="form-group" data-node-property="soma">
            <label title="Soma">Soma State</label>
            <select class="app-soma-select"></select>
        </div>

        <div class="form-group" data-node-property="magnitude">
            <label title="Magnitude">Magnitude <span
                        class="app-magnitude-label pull-right label label-default"></span></label>

            <div class="app-magnitide-slider"></div>
        </div>

        <div class="form-group" data-node-property="language">
            <label title="Language">Language</label>
            <select class="app-lang-select">
                <option value="en">English</option>
                <option value="zh">Mandarin</option>
            </select>
        </div>

        <div class="form-group" data-node-property="text">
            <label title="Text">Text</label>
            <textarea class="app-node-text form-control" title="Text"></textarea>
        </div>

        <div class="form-group" data-node-property="attention_region">
            <label>Attention region</label>
            <select class="app-attention-region-select"></select>
        </div>

        <div class="form-group" data-node-property="crosshair">
            <div class="app-crosshair"></div>
        </div>

        <div class="form-group" data-node-property="topic">
            <label>Wait for topic</label>
            <input type="text" class="app-node-topic form-control" title="Topic name"/>
        </div>

        <div class="form-group" data-node-property="timeout">
            <label>Timeout</label>
            <div class="input-group">
                <input type="number" class="app-node-timeout form-control" title="Timeout"/>
                <div class="input-group-addon">s</div>
            </div>
        </div>

        <div class="node-setting-buttons form-group">
            <div class="btn-group" role="group" aria-label="...">
                <button class="app-delete-node-button btn btn-danger"><i
                            class="glyphicon glyphicon-trash"></i>
                    Delete
                </button>
                <button class="app-node-duration-indicator btn btn-default" disabled="disabled">0s
                </button>
                <button class="app-node-frames-indicator btn btn-default" disabled="disabled">0</button>
                <button class="app-hide-settings-button btn btn-default" title="Hide node settings">
                    ×
                </button>
            </div>
        </div>
    </div>
</div>