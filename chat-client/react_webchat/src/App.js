import React, {Component} from 'react';

import './App.css';
import 'react-table/react-table.css'
import Chatroom from './Chatroom.js'
import ChatroomWithTracker from './ChatroomWithTracker.js'
import Tracker from './Tracker.js'
import TrackerNLU from './TrackerNLU.js'
import TrainingChatroom from './TrainingChatroom.js'
import Train from './Train.js'
import Domain from './Domain'
import Button from './Button'
import ConversationDownloadSection from './ConversationDownloadSection.js'
import StoryDownloadSection from './StoryDownloadSection.js'

import GlobalBroadcaster from "./GlobalBroadcaster";

class App extends Component {
    constructor(props) {
        super(props);
        let username = process.env.username || process.env.user || 'aUser';
        let params = App.getAllUrlParams();
        let screensToShow = params["tabs_to_show"] || 'all'; // all - start_plus_home - none
        let startScreen = params["start_tab"] || 'Home';
        let activeScreen = startScreen;
        let senderId = params["username"] || localStorage.getItem('senderId') || username;
        let botInstanceId = params["bot"] || localStorage.getItem('activeBotInstanceId') || 'bot-demo';
        let systemId = this.getSystemId(botInstanceId);
        let environment = params["environment"] || localStorage.getItem('active_env') || 'dev';

        let baseUrl = App.getBaseUrl(environment);
        let dialogueEndpoint = App.getDialogueEndpoint(baseUrl, botInstanceId, systemId);

        let allBotInstances = [
            {id: 'demo', repo_id: 'bot-demo', name: 'bot starter/demo'},
        ]

        let allEnvironments = [
            {id: 'dev', name: 'Development'},
            {id: 'acc', name: 'Acceptance'},
            {id: 'pro', name: 'Production'}
        ]


        this.state = {
            screensToShow: screensToShow,
            startScreen: startScreen,
            activeScreen: activeScreen,
            senderId: senderId,
            activeBotInstanceId: botInstanceId,
            active_env: environment,
            baseUrl: baseUrl,
            dialogueEndpoint: dialogueEndpoint,
            allBotInstances: allBotInstances,
            allEnvironments: allEnvironments
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSelection = this.handleSelection.bind(this);
        this.goToHome = this.goToHome.bind(this);
        this.goToChatClient = this.goToChatClient.bind(this);
        this.goToChatWithTrackers = this.goToChatWithTrackers.bind(this);
        this.goToStoryBuilder = this.goToStoryBuilder.bind(this);
        window.globalBroadcaster = new GlobalBroadcaster();
    }

    getSystemId(botInstanceId) {
        return botInstanceId.replace(/-.*/, '');
    }

    getBotFunctionalId(allBotInstances, activeBotInstanceId) {
        for (let i = 0; i < allBotInstances.length; i++) {
            let botInstance = allBotInstances[i];
            if (botInstance.id === activeBotInstanceId) {
                return botInstance.repo_id.replace(/.*-bot-/, '');
            }
        }
        return '';
    }

    // to handle Microsoft Edge v < 17...
    // based on https://www.sitepoint.com/get-url-parameters-with-javascript/
    static getAllUrlParams() {

        // we'll store the parameters here
        var obj = {};

        // get query string from url (optional) or window
        var queryString = document.location.search.slice(1);

        // if query string exists
        if (queryString) {

            // stuff after # is not part of query string, so get rid of it
            queryString = queryString.split('#')[0];

            // split our query string into its component parts
            var arr = queryString.split('&');

            for (var i = 0; i < arr.length; i++) {
                // separate the keys and the values
                var a = arr[i].split('=');

                // set parameter name and value (use 'true' if empty)
                var paramName = a[0];
                var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];

                // if the paramName ends with square brackets, e.g. colors[] or colors[2]
                if (paramName.match(/\[(\d+)?\]$/)) {

                    // create key if it doesn't exist
                    var key = paramName.replace(/\[(\d+)?\]/, '');
                    if (!obj[key]) obj[key] = [];

                    // if it's an indexed array e.g. colors[2]
                    if (paramName.match(/\[\d+\]$/)) {
                        // get the index value and add the entry at the appropriate position
                        var index = /\[(\d+)\]/.exec(paramName)[1];
                        obj[key][index] = paramValue;
                    } else {
                        // otherwise add the value to the end of the array
                        obj[key].push(paramValue);
                    }
                } else {
                    // we're dealing with a string
                    if (!obj[paramName]) {
                        // if it doesn't exist, create property
                        obj[paramName] = paramValue;
                    } else if (obj[paramName] && typeof obj[paramName] === 'string') {
                        // if property does exist and it's a string, convert it to an array
                        obj[paramName] = [obj[paramName]];
                        obj[paramName].push(paramValue);
                    } else {
                        // otherwise add the property
                        obj[paramName].push(paramValue);
                    }
                }
            }
        }

        return obj;
    }

    static logEndpoints(
        productionModeOverride,
        localProductionMode,
        botInstanceId,
        botFunctionalId,
        systemId,
        pillar,
        baseUrl,
        dialogueEndpoint,
        nluEndpoint,
        dialogueLogsEndpoint) {
        console.log("****")
        console.log("****")
        console.log("* Bot Technical ID: " + botInstanceId)
        console.log("* Bot Functional ID: " + botFunctionalId)
        console.log("* System: " + systemId)
        console.log("* Pillar: " + pillar)
        console.log("* Base URL: " + baseUrl);
        console.log("* Dialogue Endpoint: " + dialogueEndpoint);
        console.log("* NLU Endpoint: " + nluEndpoint);
        console.log("* Dialogue Logs Endpoint: " + dialogueLogsEndpoint);

        if (productionModeOverride || localProductionMode) {
            console.log("*")
            console.log("* ProductionModeOverride: " + productionModeOverride)
            console.log("* LocalProductionMode: " + localProductionMode)
        }
        console.log("****")
    }

    static getBaseUrl(environment) {
        const protocol = window.location.protocol;
        const hostAndPort = window.location.host;
        if (hostAndPort === 'localhost:3000') {
            // development or production using localhost
            return protocol + '//' + hostAndPort.replace(/:.*/, '') + "{PORT_SUFFIX}";
        } else { // production
            return 'https://production.url';
        }
    }

    static getDialogueEndpoint(baseUrl, botInstanceId) {
        let result = baseUrl;
        result = result.replace('{BOT_INSTANCE_ID}', botInstanceId);
        result = result.replace("{PORT_SUFFIX}", process.env.REACT_APP_DIALOGUE_RUN_PORT_SUFFIX);
        return result;
    }


    updateEndPoints() {
        let systemId = this.getSystemId(this.state.activeBotInstanceId);
        const baseUrl = App.getBaseUrl(this.state.active_env);
        let dialogueEndpoint = App.getDialogueEndpoint(baseUrl, this.state.activeBotInstanceId, systemId);
        let botFunctionalId = this.getBotFunctionalId(this.state.allBotInstances, this.state.activeBotInstanceId);

        this.setState({
            baseUrl: baseUrl,
            activeBotFunctionalId: botFunctionalId,
            dialogueEndpoint: dialogueEndpoint
        })
    }

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        localStorage.setItem(name, value)

        this.setState({
            [name]: value
        });
    }

    handleSelection(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        localStorage.setItem(name, value)

        this.setState({
            [name]: value
        }, () => {
            this.updateEndPoints()
        });
    }

    goToHome(event) {
        this.setState({
            activeScreen: 'Home'
        });
    }

    goToChatClient(event) {
        this.setState({
            activeScreen: 'ChatClient'
        });
    }

    goToChatWithTrackers(event) {
        this.setState({
            activeScreen: 'ChatClientDebug'
        });
    }

    goToStoryBuilder(event) {
        this.setState({
            activeScreen: 'StoryBuilder'
        });
    }


    renderChatClient(props) {
        const senderId = this.state.senderId;

        return <div>
            <div className="App chatview">
                <Chatroom senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
            </div>
        </div>
    }

    renderChatWithTrackers(props) {
        const senderId = this.state.senderId;

        return <div>
            <div className="App chatview">
                <ChatroomWithTracker senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
                <TrackerNLU senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
                <Tracker senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
            </div>
            <div className="AppConversationDownloadSection chatview">
                <ConversationDownloadSection senderId={senderId}/>
            </div>
        </div>
    }

    renderStoryBuilder(props) {
        const senderId = this.state.senderId;

        return <div>
            <div className="App chatview">
                <TrainingChatroom senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
                <Train senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
                <Domain senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
            </div>
            <div className="AppStoryDownloadSection chatview">
                <StoryDownloadSection senderId={senderId} dialogueEndpoint={this.state.dialogueEndpoint}/>
            </div>
        </div>
    }

    renderHome(props) {
        const senderId = this.state.senderId;

        let botSelectOptions = []
        for (let i = 0; i < this.state.allBotInstances.length; i++) {
            let botInstance = this.state.allBotInstances[i];
            botSelectOptions.push(<option key={botInstance.id} value={botInstance.id}>{botInstance.name}</option>)
        }

        let environmentChoices = []
        for (let i = 0; i < this.state.allEnvironments.length; i++) {
            let environment = this.state.allEnvironments[i];
            environmentChoices.push(<option key={environment.id} value={environment.id}>{environment.name}</option>)
        }

        return <div className="AppHeader">
            <div>
                <table className="botForm">
                    <tbody>
                    <tr>
                        <td>Active Bot</td>
                        <td>
                            <select name="activeBotInstanceId" defaultValue={this.state.activeBotInstanceId}
                                    onChange={this.handleSelection}>
                                {botSelectOptions}
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>Environment</td>
                        <td>
                            <select name="activeEnv" defaultValue={this.state.active_env}
                                    onChange={this.handleSelection}>
                                {environmentChoices}
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>Your ID</td>
                        <td><input name="senderId" type="text" onChange={this.handleChange} placeholder="a name"
                                   defaultValue={senderId}/></td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    }

    renderView(props) {
        if (this.state.activeScreen === 'ChatClient') {
            return this.renderChatClient(props);
        }
        else if (this.state.activeScreen === 'ChatClientDebug') {
            return this.renderChatWithTrackers(props);
        }
        else if (this.state.activeScreen === 'StoryBuilder') {
            return this.renderStoryBuilder(props);
        }
        else {
            return this.renderHome(props);
        }
    }

    renderApp(props) {
        const activeScreen = this.state.activeScreen;

        let screenSelection = <div></div>;

        if (this.state.screensToShow !== 'none') {
            let tabButtons = [];

            tabButtons.push(<Button key='Home' onClick={this.goToHome} label="Home"
                                    disabled={activeScreen === 'Home'}/>);

            tabButtons.push(<Button key='ChatClient' onClick={this.goToChatClient} label="Chat"
                                    disabled={activeScreen === 'ChatClient'}/>);

            tabButtons.push(<Button key='ChatClientDebug' onClick={this.goToChatWithTrackers}
                                    label="Chat with Trackers" disabled={activeScreen === 'ChatClientDebug'}/>);

            tabButtons.push(<Button key='StoryBuilder' onClick={this.goToStoryBuilder} label="Composer"
                                    disabled={activeScreen === 'StoryBuilder'}/>);

            screenSelection = <div className="ScreenSelectionSection">
                <div className="selectionSection">
                    <div className="TabsSpace">
                        {tabButtons}
                    </div>
                </div>
            </div>
        }


        return (
            <div>
                {screenSelection}
                <div>
                    {this.renderView()}
                </div>
            </div>
        );
    }

    render(props) {
        return this.renderApp(props);
    }
}

export default App;
