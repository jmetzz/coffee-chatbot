import ReactDOM from 'react-dom';
import './App.css';
import BaseChatroom from './BaseChatroom.js';

// BaseChatroomRun is the base class for all chatrooms that only have RUN endpoint access
class BaseChatroomRun extends BaseChatroom {
    constructor(props) {
        super(props);

        this.submitMessage = this.submitMessage.bind(this);
        this.restartButton = this.restartButton.bind(this);
        this.getConversation();
    }

    getConversation() {
        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId + "/messages";

        fetch(endpoint, {
            headers: {
                "Content-Type": "application/json",
            },
            method: "GET"
        }).then(
            result => result.json())
            .then(
                (result) => {
                    this.updateChatMessages(result);
                }
            )
            .catch(
                error => console.log('error============:', error));
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
                this.getConversation();
            }, () => {
                ReactDOM.findDOMNode(this.refs.msg).value = "";
            }
        ).catch(error => console.log('error============:', error));
    }

    restartButton() {
        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId;

        fetch(endpoint, {method: "DELETE"}).then(
            (result) => this.getConversation()
        ).catch(error => console.log('error============:', error));
    }
}

export default BaseChatroomRun;
