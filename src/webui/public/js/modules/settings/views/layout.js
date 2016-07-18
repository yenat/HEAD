define(['marionette', 'tpl!./templates/layout.tpl', 'lib/regions/fade_in', 'jquery', 'lib/api', 'underscore', 'push_menu'],
    function (Marionette, template, FadeInRegion, $, api, _) {
        return Marionette.LayoutView.extend({
            template: template,
            regions: {
                content: {
                    el: '.app-settings-container',
                    regionClass: FadeInRegion
                }
            },
            ui: {
                navigation: '.app-settings-navigation',
                nodeList: '.app-nav-node-list',
                navLinks: '.app-settings-navigation a'
            },
            events: {
                'click @ui.navLinks': 'collapseNav'
            },
            onShow: function () {
                this.ui.navigation.multilevelpushmenu({
                    menuWidth: '250px',
                    menuHeight: $(document).height(),
                    collapsed: true,
                    preventItemClick: false
                });

                $(window).on("resize", this.updateNavHeight, this);
                this.nodeListInterval = setInterval(_.bind(this.updateNodeList, this), 10000);
                this.updateNodeList();
            },
            collapseNav: function () {
                $(this.ui.navigation).multilevelpushmenu('collapse');
            },
            updateNodeList: function () {
                var self = this;
                api.services.get_configurable_nodes.callService({}, function (response) {
                    var container = $('<div>');
                    $.each(response.nodes, function () {
                        var link = $('<a>').prop({
                            href: '#/admin/settings/node/' + encodeURIComponent(this)
                        }).html(this);
                        container.append($('<li>').append(link));
                    });
                    self.ui.nodeList.html(container.html());
                }, function (error) {
                    console.log(error);
                });
            },
            updateNavHeight: function () {
                this.ui.navigation.multilevelpushmenu('option', 'menuHeight', $(document).height());
                this.ui.navigation.multilevelpushmenu('redraw');
            },
            onDestroy: function () {
                $(window).off("resize", this.updateNavHeight, this);
                clearInterval(this.nodeListInterval);
            }
        });
    });
