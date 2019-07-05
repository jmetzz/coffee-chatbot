import React from 'react';
import './App.css';
import ReactTable from 'react-table'

class TrackerNLU extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tracker: undefined,
            trainingStatus: '...'
        }

        this.updateTrackerInfo = this.updateTrackerInfo.bind(this);
        window.globalBroadcaster.subscribe('update_tracker_info', this.updateTrackerInfo);
    }

    componentWillUnmount() {
        window.globalBroadcaster.unsubscribe('update_tracker_info', this.updateTrackerInfo);
    }

    updateTrackerInfo(tracker, entityData, intentRanking, slotData, eventData) {
        this.setState({
            tracker: tracker,
            entityData: entityData,
            intentRanking: intentRanking
        })
    }

    render() {
        const entityColumns = [{
            Header: 'Entity',
            accessor: 'entity', // String-based value accessors!
            headerClassName: 'columnheader'
        }, {
            Header: 'Mapped value',
            accessor: 'value',
            headerClassName: 'columnheader'
        }, {
            Header: 'confidence',
            accessor: 'confidence',
            headerClassName: 'columnheader'
        }];
        const intentRankingColumns = [{
            Header: 'Intent',
            accessor: 'name',
            headerClassName: 'columnheader'
        }, {
            Header: 'confidence',
            accessor: 'confidence',
            headerClassName: 'columnheader'
        }];

        return (
            <div className="tracker">
                <h3>Tracker NLU</h3>
                <ReactTable
                    data={this.state.entityData}
                    columns={entityColumns}
                    defaultPageSize={6}
                    noDataText="No entities found"
                />
                <ReactTable
                    data={this.state.intentRanking}
                    columns={intentRankingColumns}
                    defaultPageSize={6}
                    noDataText="No intents found"
                />
            </div>
        );
    }
}

export default TrackerNLU;
