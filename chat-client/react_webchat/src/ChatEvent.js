import React from 'react';

const ChatEvent = ({event, index}) => ( parse(event, index) );

function parse(event, index) {
    if (event.event === "slot"){
        return <li className="event left" key={index}>variable {event.name} : {event.value}</li>
    }

    if (event.event === "action") {
        return <li className="event left" key={index}>{event.name}</li>
    }

    if (event.event === "bot") {
        return <li className="bot event left message" key={index}><p>{event.text}</p></li>
    }

    if (event.event === "user") {
        let entities = [];
        for (var i = 0; i < event.parse_data.entities.length; i++) {
            let entity = event.parse_data.entities[i];
            entities.push(
                <li className="user event right" key={index}>
                    entity: {entity.entity}: {entity.value} ({entity.confidence.toFixed(2)})
                </li>);
        }

        return <div key={index}>
                <li className="user event right message">
                    <p> {event.text} </p>
                </li>
                <li className="user event right">
                    intent: {event.parse_data.intent.name} ({event.parse_data.intent.confidence.toFixed(2)})
                </li>
                {entities}
            </div>
    }

    // make sure there is always a return!
    return <li className="event left" key={index}>{event.event}</li>
}

export default ChatEvent;
