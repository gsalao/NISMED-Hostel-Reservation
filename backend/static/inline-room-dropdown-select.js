$(document).ready(function () {
    function setupInlineRow($row) {
        
        // looks for all the table rows
        const $roomType = $row.find('select[id$="-room_type"]');
        const $room = $row.find('select[id$="-room"]');
        const $rate = $row.find('select[id$="-room_rate"]');

        const fetchAndPopulate = () => {
            const roomTypeId = $roomType.val();
            const currentRoom = $room.val();
            const currentRate = $rate.val();

            if (!roomTypeId) return;

            // Fetch Rooms
            $.ajax({
                url: `/api/room/rooms/?room_type_id=${roomTypeId}`,
                success: function (data) {
                    $room.empty().append('<option value="">---------</option>');
                    let matchFound = false;
                    data.forEach(room => {
                        if (room.is_active) {
                            const selected = currentRoom == room.id;
                            if (selected) matchFound = true;
                            $room.append(`<option value="${room.id}" ${selected ? "selected" : ""}>${room.str}</option>`);
                        }
                    });
                    if (!matchFound && currentRoom) {
                        $room.append(`<option value="${currentRoom}" selected>(Unavailable Room)</option>`);
                    }
                }
            });

            // Fetch Room Rates
            $.ajax({
                url: `/api/room/rates/?room_type_id=${roomTypeId}`,
                success: function (data) {
                    $rate.empty().append('<option value="">---------</option>');
                    let rateMatch = false;
                    data.forEach(rate => {
                        const selected = currentRate == rate.id;
                        if (selected) rateMatch = true;
                        $rate.append(`<option value="${rate.id}" ${selected ? "selected" : ""}>${rate.str}</option>`);
                    });
                    if (!rateMatch && currentRate) {
                        $rate.append(`<option value="${currentRate}" selected>(Unavailable Rate)</option>`);
                    }
                }
            });
        };

        // Bind change event
        $roomType.off('change.inlineBind').on('change.inlineBind', fetchAndPopulate);

        // Initial call
        if ($roomType.val()) {
            fetchAndPopulate();
        }
    }

    // Calls the setupInlineRow function to each of the existing rows
    $('tr[id^="reservedroom_set-"]').each(function () {
        setupInlineRow($(this));
    });

    // this "listens" to when the page is loaded and adds an event listener to the add links button and calls the setupInlineRow function when 
    // a new row is added
    window.addEventListener("load", function () {
        const addLinks = document.getElementsByClassName('addlink');

        for (let i = 0; i < addLinks.length; i++) {
            addLinks[i].addEventListener("click", function () {
                const $allRows = $('tr[id^="reservedroom_set-"]').not('[id$="-empty"]');
                const $newRow = $allRows.last();
                setupInlineRow($newRow);
            });
        }
    });
});
