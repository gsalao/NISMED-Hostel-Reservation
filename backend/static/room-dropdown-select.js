
$(document).ready(function () {
    console.log("Custom admin JS loaded!");

    $('#id_room_type').change(function () {
        const roomTypeId = $(this).val();
        console.log("Room Type changed to:", roomTypeId);

        if (roomTypeId) {
            // Get Rooms filtered by RoomType
            $.ajax({
                url: `/api/room/rooms/?room_type_id=${roomTypeId}`,
                success: function (data) {
                    let roomOptions = '<option value selected>---------</option>';
                    $.each(data, function (index, room) {
                        if (room.is_active) {
                          roomOptions += `<option value="${room.id}">${room.str}</option>`;
                        } 
                    });
                    $('#id_room').html(roomOptions);
                }
            });

            // Get RoomRates filtered by RoomType
            $.ajax({
                url: `/api/room/rates/?room_type_id=${roomTypeId}`,
                success: function (data) {
                    let rateOptions = '<option value selected>---------</option>';
                    $.each(data, function (index, rate) {
                        rateOptions += `<option value="${rate.id}">${rate.str}</option>`;
                    });
                    $('#id_room_rate').html(rateOptions);
                }
            });
        }
    });
});
