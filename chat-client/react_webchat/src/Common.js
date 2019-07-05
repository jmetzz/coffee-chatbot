class Common  {
    static update_tracker_info(tracker_info) {
        window.globalBroadcaster.dispatch('update_tracker_info', tracker_info);
    }

    static publish_prediction(prediction) {
        window.globalBroadcaster.dispatch('publish_prediction', prediction);
    }

    static confirm_action() {
        window.globalBroadcaster.dispatch('confirm_action');
    }

    static trigger_fetch_domain() {
        window.globalBroadcaster.dispatch('trigger_fetch_domain');
    }
}

export default Common;
