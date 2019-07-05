import './App.css';
import BaseChatroomUI from './BaseChatroomUI.js';
import Common from './Common'

class ChatroomWithTracker extends BaseChatroomUI {

    getTitle() {
        return "Chat with Trackers";
    }

    updateTrackerInfo(tracker_info) {
        Common.update_tracker_info(tracker_info);
    }
}

export default ChatroomWithTracker;
