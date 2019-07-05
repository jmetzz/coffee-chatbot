import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Button from './Button'
import Common from './Common'
import ChatEvent from './ChatEvent.js';

class TrainingChatroom extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            events: []
        };

        this.submitMessage = this.submitMessage.bind(this);
        this.predictMessage = this.predictMessage.bind(this);
        this.restartButton = this.restartButton.bind(this);

        window.globalBroadcaster.subscribe('restart', this.restartButton);
        window.globalBroadcaster.subscribe('confirm_action', this.predictMessage);

        this.predictMessage();
    }

    componentDidMount() {
        this.scrollToBot();
    }

    componentDidUpdate() {
        this.scrollToBot();
    }

    componentWillUnmount() {
        window.globalBroadcaster.unsubscribe('restart', this.restartButton);
        window.globalBroadcaster.unsubscribe('confirm_action', this.predictMessage);
    }

    scrollToBot() {
        ReactDOM.findDOMNode(this.refs.events).scrollTop = ReactDOM.findDOMNode(
            this.refs.events).scrollHeight;
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
                skipExecution: true
            }),
            headers: {
                "Content-Type": "application/json",
            },
            method: "POST"
        }).then(
            result => result.json())
            .then(
                (result) => {
                    this.predictMessage()
                }
            )
            .catch(
                error => console.log('[ERROR]', error));
    }


    predictMessage() {
        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId + "/prediction";

        fetch(endpoint, {
            headers: {"Content-Type": "application/json",},
            method: "GET"
        }).then(
            result => result.json())
            .then(
                (result) => {
                    this.setState({events: result.tracker.events,},
                        () => {
                            ReactDOM.findDOMNode(this.refs.msg).value = "";
                        })

                    Common.publish_prediction([result])
                }
            )
            .catch(
                error => console.log('[ERROR]', error));
    }

    restartButton() {
        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId;

        fetch(endpoint, {method: "DELETE"}).then(
            (result) => {
                this.predictMessage();
                this.fillDomain();
            }
        ).catch(error => console.log('error============:', error));
    }

    fillDomain() {
        Common.trigger_fetch_domain();
    }

    render() {
        const {events} = this.state;
        const senderId = this.props.senderId;
        const lastEvent = events[events.length - 1];
        const enabled = lastEvent && lastEvent.event === "action" && lastEvent.name === "action_listen";

        return (
            <div className="chatroom">
                <h3>Story Builder</h3>
                <div className="buttonSpace">
                    <span className="senderlabel">{senderId}</span>
                    <Button onClick={this.restartButton} label="restart"/>
                </div>
                <ul className="events" ref="events">
                    {
                        events.map((event, i) =>
                            <ChatEvent key={i} index={i} event={event}/>
                        )
                    }
                </ul>
                <form className="input" onSubmit={(e) => this.submitMessage(e)}>
                    <input type="text" ref="msg" disabled={!enabled}/>
                    <input type="submit" value="Send" disabled={!enabled}/>
                </form>
            </div>
        );
    }
}

export default TrainingChatroom;
