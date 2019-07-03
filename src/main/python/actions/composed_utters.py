from .action_composed_utter import ActionComposedUtter

ActionAfspraakBeheren = type("ActionScheduleAppointment",
                             (ActionComposedUtter,),
                             {"utter_list": ["utter_schedule_appointment", "utter_appointment_page"],
                              "action_name": "action_schedule_appointment"})
