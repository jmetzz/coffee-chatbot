import React from 'react';
import './App.css';
import 'react-select/dist/react-select.css';
import Button from './Button'
import Common from './Common'

class Train extends React.Component {
    constructor(props) {
        super(props);

        this.state = {scores: []}

        this.update_score_data = this.update_score_data.bind(this);
        this.confirmAction = this.confirmAction.bind(this);

        window.globalBroadcaster.subscribe('publish_prediction', this.update_score_data);
    }

    componentWillUnmount() {
        window.globalBroadcaster.unsubscribe('publish_prediction', this.update_score_data);
    }

    update_score_data(prediction) {
        const lastEvent = prediction.tracker.events[prediction.tracker.events.length - 1];
        const hide_data = lastEvent && lastEvent.event === "action" && lastEvent.name === "action_listen";
        let data = hide_data ? [] : prediction.scores;

        this.setState({scores: data});
    }


    confirmAction(nextAction) {
        let endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId + "/actions";

        fetch(endpoint, {
            body: JSON.stringify({name: nextAction, channelId: 'chatclient'}),
            headers: {
                "Content-Type": "application/json",
            },
            method: "POST"
        }).then(
            result => {
                Common.confirm_action();
            }
        ).catch(error => console.log('[ERROR]:', error));
    }

    render() {
        let {scores} = this.state;

        scores.sort((a, b) => b.score - a.score)
        const next_action = scores.shift();
        const action_name = next_action ? next_action.action : undefined;
        const action_score = next_action ? "(" + next_action.score.toFixed(2) + ")" : undefined;

        return (
            <div className="train">
                <h3>Confirmation</h3>

                {(next_action) ?
                    <div className="bigbutton">
                        <h2>Action: {action_name} {action_score}</h2>
                        <Button onClick={() => this.confirmAction(action_name)} label="Confirm"/>
                    </div>
                    : <span></span>
                }

                <br/>

                {(scores.length > 0) ?
                    <h2>Alternative actions</h2> : <span></span>
                }

                <div ref="scores">
                    {
                        scores.map((s, k) =>
                            <div key={k}>
                                <Button onClick={() => this.confirmAction(s.action)}
                                        label={s.action + " (" + s.score.toFixed(2) + ")"}/>
                            </div>
                        )
                    }
                </div>

            </div>
        );
    }
}

export default Train;
