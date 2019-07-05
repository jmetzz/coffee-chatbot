import React from 'react';
import './App.css';

class StoryDownloadSection extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            events: []
        };
    }

    render() {
        let endpoint;
        endpoint = this.props.dialogueEndpoint + "/api/v2/sessions/" + this.props.senderId + "/story";

        return (
            <div className="downloadLinkSection">
                <a className="downloadlink story" href={endpoint}>
                    Download story file
                </a>
            </div>
        );
    }
}

export default StoryDownloadSection;
