$(document).ready(function () {
    const pathParts = window.location.pathname.split('/');
    const reservationId = pathParts[pathParts.length - 3];

    const roomCache = new Map();
    const rateCache = new Map();

    const requestQueue = [];
    let isProcessingQueue = false;

    function enqueueRequest(fn) {
        requestQueue.push(fn);
        if (!isProcessingQueue) {
            processQueue();
        }
    }

    function processQueue() {
        if (requestQueue.length === 0) {
            isProcessingQueue = false;
            return;
        }
        isProcessingQueue = true;
        const fn = requestQueue.shift();
        fn().finally(() => processQueue());
    }

    function setupInlineRow($row) {
        const $roomType = $row.find('select[id$="-room_type"]');
        const $room = $row.find('select[id$="-room"]');
        const $rate = $row.find('select[id$="-room_rate"]');

        const fetchAndPopulate = () => {
            const roomTypeId = $roomType.val();
            const currentRoom = $room.val();
            const currentRate = $rate.val();
            if (!roomTypeId) return;

            // Fetch Rooms
            enqueueRequest(() => {
                return new Promise((resolve) => {
                    if (roomCache.has(roomTypeId)) {
                        populateRooms(roomCache.get(roomTypeId), $room, currentRoom);
                        resolve();
                    } else {
                        $.get(`/api/room/rooms/?room_type_id=${roomTypeId}&reservation=${reservationId}`, function (data) {
                            roomCache.set(roomTypeId, data);
                            populateRooms(data, $room, currentRoom);
                            resolve();
                        });
                    }
                });
            });

            // Fetch Rates
            enqueueRequest(() => {
                return new Promise((resolve) => {
                    if (rateCache.has(roomTypeId)) {
                        populateRates(rateCache.get(roomTypeId), $rate, currentRate);
                        resolve();
                    } else {
                        $.get(`/api/room/rates/?room_type_id=${roomTypeId}`, function (data) {
                            rateCache.set(roomTypeId, data);
                            populateRates(data, $rate, currentRate);
                            resolve();
                        });
                    }
                });
            });
        };

        $roomType.off('change.inlineBind').on('change.inlineBind', fetchAndPopulate);

        if ($roomType.val()) {
            fetchAndPopulate();
        }
    }

    function populateRooms(data, $room, currentRoom) {
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

    function populateRates(data, $rate, currentRate) {
        $rate.empty().append('<option value="">---------</option>');
        let matchFound = false;
        data.forEach(rate => {
            const selected = currentRate == rate.id;
            if (selected) matchFound = true;
            $rate.append(`<option value="${rate.id}" ${selected ? "selected" : ""}>${rate.str}</option>`);
        });
        if (!matchFound && currentRate) {
            $rate.append(`<option value="${currentRate}" selected>(Unavailable Rate)</option>`);
        }
    }

    // Initial setup for all rows
    $('tr[id^="reservedroom_set-"]').not('[id$="-empty"]').each(function () {
        setupInlineRow($(this));
    });

    // Listen for added inline rows
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
