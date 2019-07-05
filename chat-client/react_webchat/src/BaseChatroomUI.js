import ReactDOM from 'react-dom';
import './App.css';
import BaseChatroom from './BaseChatroom.js';

// BaseChatroomUI is the base class for all chatrooms that have UI endpoint access
class BaseChatroomUI extends BaseChatroom {
    constructor(props) {
        super(props);

        this.submitMessage = this.submitMessage.bind(this);
        this.restartButton = this.restartButton.bind(this);
        this.getTrackerInfoAndUpdate();
    }

    getTrackerInfoAndUpdate() {
        let endpoint = this.props.dialogueEndpoint + '/api/v2/sessions/' + this.props.senderId + "/tracker";

        fetch(endpoint, {
            headers: {
                "Content-Type": "application/json",
            },
            method: "GET"
        }).then(
            result => result.json())
            .then(
                (result) => {

                    var isUpdateMessageRetrieved = (result !== undefined);

                    var isEntityRetrieved = (
                        result !== undefined
                        && result.latest_message !== undefined);

                    var isIntentRetrieved = (
                        result !== undefined
                        && result.latest_message !== undefined
                        && result.latest_message.intent_ranking !== undefined);

                    var entityData = [];
                    if (isEntityRetrieved) {
                        entityData = result.latest_message.entities;
                    }

                    var intentRanking = [];
                    if (isIntentRetrieved) {
                        intentRanking = result.latest_message.intent_ranking;
                    }

                    var slots = [];
                    for (var slotKey in result.slots) {
                        if (result.slots.hasOwnProperty(slotKey)) {
                            slots.push({slotName: slotKey, slotValue: result.slots[slotKey]})
                        }
                    }

                    var slotData = [];
                    var eventData = [];
                    if (isUpdateMessageRetrieved) {
                        slotData = slots;
                        eventData = result.events;
                    }

                    this.updateChatMessages(eventData);

                    var tracker_info = [result, entityData, intentRanking, slotData, eventData];
                    this.updateTrackerInfo(tracker_info);
                }
            )
            .catch(
                error => console.log('error============:', error));
    }

    updateTrackerInfo(tracker_info) {
    }

    submitMessage(e) {
        e.preventDefault();
        var userMessage = ReactDOM.findDOMNode(this.refs.msg).value;
        ReactDOM.findDOMNode(this.refs.msg).value = "";

        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId + "/messages";

        fetch(endpoint, {
            body: JSON.stringify({
                message: userMessage,
                channelId: 'chatclient',
                skipExecution: false
            }),
            headers: {
                "Content-Type": "application/json",
            },
            method: "POST"
        }).then(
            result => result.json()
        ).then(
            (result) => {
                this.getTrackerInfoAndUpdate();
                this.messageSubmitted();
            }, () => {
                ReactDOM.findDOMNode(this.refs.msg).value = "";
            }
        ).catch(error => console.log('error============:', error));
    }

    restartButton() {
        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId;

        fetch(endpoint, {method: "DELETE"}).then(
            (result) => this.getTrackerInfoAndUpdate()
        ).catch(error => console.log('error============:', error));
    }

    restarted() {
    }
}

export default BaseChatroomUI;
