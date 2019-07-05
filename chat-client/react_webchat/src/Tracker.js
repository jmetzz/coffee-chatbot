import React from 'react';

import './App.css';
import ReactTable from 'react-table'

class Tracker extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tracker: undefined,
            slots: undefined,
            trainingStatus: '...'
        }

        this.updateTrackerInfo = this.updateTrackerInfo.bind(this);
        window.globalBroadcaster.subscribe('update_tracker_info', this.updateTrackerInfo);
    }

    componentDidMount() {
    }

    componentWillUnmount() {
        window.globalBroadcaster.unsubscribe('update_tracker_info', this.updateTrackerInfo);
    }

    updateTrackerInfo(tracker, entityData, intentRanking, slotData, eventData) {
        this.setState({
        tracker: tracker,
        slotData: slotData,
        eventData: eventData
        })
    }

    render() {
        const slotColumns = [{
            Header: 'Slot name',
            accessor: 'slotName', // String-based value accessors!
            headerClassName: 'columnheader'
        }, {
            Header: 'Slot value',
            accessor: 'slotValue',
            headerClassName: 'columnheader'
        }];
        const eventColumns = [{
            Header: 'Event',
            accessor: 'event',
            headerClassName: 'columnheader',
            minWidth: 50
        }
        , {
            Header: 'Text',
            accessor: 'text',
            headerClassName: 'columnheader'
        }, {
            Header: 'Name',
            accessor: 'name',
            headerClassName: 'columnheader'
        }, {
            Header: 'Value',
            accessor: 'value',
            headerClassName: 'columnheader'
        }];
        return (
            <div className="tracker">
                <h3>Tracker Core</h3>
                <ReactTable
                    data={this.state.slotData}
                    columns={slotColumns}
                    defaultPageSize={6}
                    noDataText="No slots found"
                />
                <ReactTable
                    data={this.state.eventData}
                    columns={eventColumns}
                    defaultPageSize={6}
                    noDataText="No events found"
                />
            </div>

        );
    }
}

export default Tracker;
