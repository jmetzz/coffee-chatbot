import React from 'react';
import './App.css';
import {CSVLink} from 'react-csv';

class ConversationDownloadSection extends React.Component {
    constructor(props) {
        super(props);

        this.fileNamePrefix = this.getDateAsString(new Date(), '_', '_', '_');

        this.state = {
            events: []
        };

        this.updateTrackerInfo = this.updateTrackerInfo.bind(this);
        window.globalBroadcaster.subscribe('update_tracker_info', this.updateTrackerInfo);
    }

    componentWillUnmount() {
        window.globalBroadcaster.unsubscribe('update_tracker_info', this.updateTrackerInfo);
    }

    getDateAsString(date, dateSeparator, dateTimeSeparator, timeSeparator) {
        var year = date.getFullYear();
        var month = date.getMonth() + 1; //Month from 0 to 11
        var day = date.getDate();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();

        return '' + year + dateSeparator +
            (month<=9 ? '0' + month : month) + dateSeparator +
            (day <= 9 ? '0' + day : day) + dateTimeSeparator +
            (hours<=9 ? '0' + hours : hours) + timeSeparator +
            (minutes <= 9 ? '0' + minutes : minutes) + timeSeparator +
            (seconds <= 9 ? '0' + seconds : seconds);
    }

    updateTrackerInfo(tracker, entityData, intentRanking, slotData, eventData) {
        var events = [];

        if (tracker !== undefined && tracker.events !== undefined) {
            for (let i = 0; i < tracker.events.length; i++) {
                var event = tracker.events[i];
                if (event.event === "action") {
                    if (event.name !== "action_listen" && !event.name.startsWith('utter_')) {
                        events.push(event);
                    }
                } else {
                    events.push(event);
                }
            }
        }

        this.setState({
            events: events
        });
    }

    render() {
        const csvHeaders = [
            {label: 'Timestamp', key: 'timestamp'},
            {label: 'Event', key: 'event'},
            {label: 'Text', key: 'text'},
            {label: 'Intent', key: 'intent'},
            {label: 'Confidence', key: 'confidence'},
            {label: 'Entities', key: 'entities'},
            {label: 'Data', key: 'data'}
        ];

        var csvData =[];
        for (let i = 0; i < this.state.events.length; i++) {
            var event = this.state.events[i];
            var timestampString = this.getDateAsString(new Date(event.timestamp * 1000), '/', ' ', ':');
            if (event.event === "action") {
                csvData.push({
                    timestamp: timestampString,
                    event: event.name
                });
            }
            else if (event.event === "user") {
                var intent;
                var confidence;
                var entitiesAsText;
                if (event.parse_data !== undefined) {
                    intent = event.parse_data.intent.name;
                    confidence = event.parse_data.intent.confidence;
                    var logEntities = [];
                    for (let i = 0; i < event.parse_data.entities.length; i++) {
                        var entity = event.parse_data.entities[i];
                        logEntities.push(entity.entity + "=" + entity.value + "(" + entity.confidence + ")");
                    }
                    entitiesAsText = logEntities.join(';');
                }
                csvData.push({
                    timestamp: timestampString,
                    event: "User " + this.props.senderId + " says",
                    text: event.text,
                    intent: intent,
                    confidence: confidence,
                    entities: entitiesAsText
                });
            }
            else if (event.event === "bot") {
                csvData.push({
                    timestamp: timestampString,
                    event: "bot says",
                    text: event.text
                });
            }
            else if (event.event === "slot") {
                csvData.push({
                    timestamp: timestampString,
                    event: "set variable",
                    data: event.name + "=" + event.value
                });
            }
        }

        const fileName = this.fileNamePrefix + "_" + this.props.senderId + "_chatlog.csv";

        return (
            <div className="downloadLinkSection">
                <CSVLink data={csvData} headers={csvHeaders} filename={fileName} className="downloadlink" target="_blank">Download this conversation as {fileName} ({csvData.length} lines)</CSVLink>
            </div>
        );
    }
}

export default ConversationDownloadSection;
