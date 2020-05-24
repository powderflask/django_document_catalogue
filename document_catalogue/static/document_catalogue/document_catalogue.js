/**
 * Configure DocumentCatalogueManager inline catalogue management capabilities.
 *  - Dropzone on document catalogue categories so a drag-drop to a category results in file upload
 *  - Ajax Delete interactions for documents
 * Dependencies:
 *   - jquery
 *   - dropzone
 */
$(document).ready(function() {

    /*
     * CSRF Token:
     *  - provide service for other modules that need the CSRFToken header
     *  - ensure the CSRF Header is set globally for all AJAX requests.
     */
    let AjaxCSRFtokenManager = {

        // Utility to set the CSRF cookie in AJAX header -- should probably be moved somewhere more generic?
        // From: https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax
        _getCookie: function(name) {
            let cookieValue = null;
            if (document.cookie) {
                let cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    let cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },

        csrfSafeMethod: function(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },

        getRequestHeader: function() {
            return {"X-CSRFToken": this._getCookie('csrftoken')}
        },

        setRequestHeader: function(xhr, method, crossDomain) {
            if (!this.csrfSafeMethod(method) && !crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", this._getCookie('csrftoken'));
            }

        }
    };

    /*
     * Micro-AJAX framework - simplified API to wrap jquery AJAX requests
     */
    let AjaxRequest = {
        make_request: function(target, args) {
            var self = this,
                ajax_events = {
                    headers: AjaxCSRFtokenManager.getRequestHeader(),
                    method: 'POST',
                    error: function (xhr, textStatus, errorThrown) {
                        el = $('div');
                        el.html = '<div class="error">We encountered an error processing request: ' + textStatus + '</div>';
                        target.after($(el));
                        console.log(xhr.status + ": " + xhr.responseText);
                        console.log(errorThrown);
                    },
                };

            $.ajax($.extend(ajax_events, args));
        },


        // Make a DELETE ajax request for the target element
        _confirmDelete: function ( event ) {
            return confirm("Delete this Document? (Action cannot be undone)");
        },

        delete : function(target, settings) {
            if (this._confirmDelete()) {

                let args = Object.create(settings);
                args.method = settings.method || 'DELETE';
                args.url = settings.url || settings.action;
                args.success = function (xhr, textStatus) {
                    target.closest('.dc-document-item').remove();
                    if (settings.success_url)
                        window.location.replace(settings.success_url);
                };
                console.assert(args.url, "ajaxDelete Error: a url must be supplied.");

                // console.log('About to ajax delete', args);  // sanity check
                this.make_request(target, args);
            }
        },
    };

    /*
     * File Upload via Dropzone:  https://www.dropzonejs.com/
     * Configure drag-drop functionality for document categories for quick file upload
     *  - uploads are configured only when a #DocumentCatalogueManager DOM element is present
     *  - uploads are configured on DOM elements with:  class='dc-dropzone'
     *  - data-url='/absolute/url/for/upload/post'  MUST be supplied in DOM
     * Any dropzone options can be added over overridden via:  data-optionName=optionValue
     *    on either #DocumentCatalogueManager element or .dc-dropzone elements
     */
    let DocumentCatalogueManager = {

        base_dropzone_options: {
            // url option MUST be supplied for the upload manager to do anything useful...
            url: '',
            // base option default values:
            paramName: 'file',                      // must match form field name on backend!
            headers: AjaxCSRFtokenManager.getRequestHeader(),
            init: function () {
                this.on("success", function (file, response) {
                    // console.log(response);  // sanity check
                    let document_item = response.document_item;
                    let target = $(file.previewTemplate).closest('.dc-category-list').find('> .dc-document-list');
                    target.append(document_item);
                    target.find('.dc-document-item:last-child .dc-document-link').addClass('text-success');
                });
            }
        },

        // loaded from DOM during configuration.
        default_dropzone_options: {},

        _get_dropzone_options: function(element) {
            // Grab dropzone option values for given DOM element or selector
            let element_options = $(element).data();
            return $.extend(this.default_dropzone_options, element_options);
        },

        configure_dropzone_uploads: function() {
            // console.log("Configuring dropzone with base options:", this.default_dropzone_options)  // sanity check
            Dropzone.autoDiscover = false;
            let self = this;
            $(".dc-dropzone").each(function() {
                $(this).dropzone(self._get_dropzone_options(this));
                $(this).addClass('dropzone');
            });
        },

        configure_ajax_delete: function() {
          $(".dc-document-delete").click(function(event) {
              let settings = {
                  url: $(event.currentTarget).data('url'),
                  success_url: $(event.currentTarget).data('successUrl'),
              };
              // console.log("Deleting doc with settings: ", settings)  // sanity check
              AjaxRequest.delete($(this), settings);
          });
        },

        configure: function () {
            // Manager component can supply default dropzone options via data- attributes
            this.default_dropzone_options = $.extend(this.base_dropzone_options, $('#DocumentCatalogueManager').data());
            this.configure_dropzone_uploads();
            this.configure_ajax_delete();
        }
    }; // DocumentManager

    // Main
    if ($('#DocumentCatalogueManager').length > 0)  // only applies if a DocumentManager component is found in the markup.
        DocumentCatalogueManager.configure();

    // Select2 Ajax Search
    $('.select2-ajax-search').select2({
        placeholder: 'Start typing to find Document',
        ajax: {
            url:  $('.select2-ajax-search').data('url'),
            processResults: function (data) {
                // Transforms the top-level key of the response object from 'items' to 'results'
                return {
                    results: data.options
                };
            }
        },
    });
    // Load-on-change: select widgets that act as drop-down menus
    $("select.load-on-change").change(function() {
        //alert('selected: ' + $(this).val());
        window.location.href = $(this).val();
    });

});