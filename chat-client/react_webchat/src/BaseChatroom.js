import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Button from './Button'
import Message from './Message.js';

class BaseChatroom extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            chats: []
        };
    }

    componentDidMount() {
        this.scrollToBot();
    }

    componentDidUpdate() {
        this.scrollToBot();
    }

    scrollToBot() {
        ReactDOM.findDOMNode(this.refs.chats).scrollTop = ReactDOM.findDOMNode(
            this.refs.chats).scrollHeight;
    }

    updateChatMessages(events) {
        var chatMessages = [];
        if (events) {
            for (var i = 0; i < events.length; i++) {
                var event = events[i];

                if (event.event === "bot") {
                    chatMessages.push({
                        username: "Chatbot",
                        content: <p>{event.text}</p>
                    });
                }

                if (event.event === "user") {
                    chatMessages.push({
                        username: "User",
                        content: <p>{event.text}</p>
                    });
                }
            }
        }

        this.setState({
            chats: chatMessages
        });
    }

    getTitle() {
        return "Chat Client";
    }

    render() {
        const title = this.getTitle()
        const username = "User";
        const {chats} = this.state;
        const senderId = this.props.senderId;

        return (
            <div className="chatroom">
                <h3>{title}</h3>
                <div className="buttonSpace">
                <span className="senderlabel">{senderId}</span>
                <Button onClick={this.restartButton} label="Restart"/>
            </div>
            <ul className="chats" ref="chats">
                {
                    chats.map((chat, i) =>
                        <Message key={i} chat={chat} user={username}/>
                    )
                }
            </ul>
            <form className="input" onSubmit={(e) => this.submitMessage(e)}>
                <input type="text" ref="msg"/>
                <input type="submit" value="Send"/>
            </form>
        </div>
        );
    }
}

export default BaseChatroom;
