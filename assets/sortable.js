htmx.onLoad(function (content) {
    var sortables = content.querySelectorAll(".sortable");
    console.log(sortables);
    for (var i = 0; i < sortables.length; i++) {
        var sortable = sortables[i];
        var sortableInstance = new Sortable(sortable, {
            animation: 150,
            fallbackOnBody: true,
            group: 'nested',
            dragoverBubble: false,
            removeCloneOnHide: false,
            handle: ".handle",

            // Make the `.htmx-indicator` unsortable
            filter: ".htmx-indicator",
            onStart: function (evt) {
            },
            onMove: function (evt) {
                return evt.related.className.indexOf('htmx-indicator') === -1;
            },

            // Disable sorting on the `end` event
            onEnd: function (evt) {
                console.log(evt);


                var new_parent_id = evt.to.dataset.id;

                var new_prev_id = null;
                var new_next_id = null;
                if (evt.newIndex != 0) {
                    new_prev_id = evt.to.children[evt.newIndex - 1].dataset.id;
                }
                if (evt.newIndex != evt.to.childElementCount - 1) {
                    new_next_id = evt.to.children[evt.newIndex + 1].dataset.id;
                }

                console.log(new_parent_id, new_prev_id, new_next_id);
                // Construct the drag and drop payload
                var payload = {
                    id: evt.item.dataset.id,
                    new_parent_id: new_parent_id,
                    new_prev_id: new_prev_id,
                    new_next_id: new_next_id
                };

                // Send via HTMX ajax
                htmx.ajax('POST', '/dnd', {
                    target: evt.item,
                    swap: 'none',
                    values: payload
                });
            }
        });

        // // Re-enable sorting on the `htmx:afterSwap` event
        // sortable.addEventListener("htmx:afterSwap", function () {
        //     sortableInstance.option("disabled", false);
        // });
    }
})