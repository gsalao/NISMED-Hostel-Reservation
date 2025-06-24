
$(document).ready(function () {
    console.log("Custom admin JS loaded!");

    const roomTypeField = $('#id_room_type');

    // Trigger on startup if already selected
    if (roomTypeField.val()) {
        console.log("Initial Room Type detected:", roomTypeField.val());
        loadDependentFields(roomTypeField.val());
    }

    // On change
    roomTypeField.change(function () {
        const roomTypeId = $(this).val();
        console.log("Room Type changed to:", roomTypeId);
        if (roomTypeId) {
            loadDependentFields(roomTypeId);
        } else {
            // Clear room and rate fields if no room type selected
            $('#id_room').html('<option value="">---------</option>');
            $('#id_room_rate').html('<option value="">---------</option>');
        }
    });

    function loadDependentFields(roomTypeId) {
        const currentRoom = $('#id_room').val();
        const currentRate = $('#id_room_rate').val();

        // Load filtered Rooms
        $.ajax({
            url: `/api/room/rooms/?room_type_id=${roomTypeId}`,
            success: function (data) {
                let roomOptions = '<option value="">---------</option>';
                let foundMatch = false;

                $.each(data, function (_, room) {
                    if (room.is_active) {
                        const selected = room.id == currentRoom ? 'selected' : '';
                        if (selected) foundMatch = true;
                        roomOptions += `<option value="${room.id}" ${selected}>${room.str}</option>`;
                    }
                });

                if (!foundMatch && currentRoom) {
                    roomOptions += `<option value="${currentRoom}" selected>(Unavailable room)</option>`;
                }

                $('#id_room').html(roomOptions);
            }
        });

        // Load filtered Room Rates
        $.ajax({
            url: `/api/room/rates/?room_type_id=${roomTypeId}`,
            success: function (data) {
                let rateOptions = '<option value="">---------</option>';
                let foundRate = false;

                $.each(data, function (_, rate) {
                    const selected = rate.id == currentRate ? 'selected' : '';
                    if (selected) foundRate = true;
                    rateOptions += `<option value="${rate.id}" ${selected}>${rate.str}</option>`;
                });

                if (!foundRate && currentRate) {
                    rateOptions += `<option value="${currentRate}" selected>(Unavailable rate)</option>`;
                }

                $('#id_room_rate').html(rateOptions);
            }
        });
    }
});
