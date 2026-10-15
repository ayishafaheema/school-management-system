document.addEventListener("DOMContentLoaded", function () {

    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: "dayGridMonth",

        headerToolbar: {
            left: "prev,next",
            center: "title",
            right: ""
        },

        dayMaxEventRows: true,

        events: [

            {
                title: "Exam",
                start: "2026-07-15"
            },

            {
                title: "Assignment",
                start: "2026-07-22"
            }

        ]

    });

    calendar.render();

});