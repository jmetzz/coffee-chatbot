import React from 'react';
import './App.css';
import 'react-tabs/style/react-tabs.css';
import {Tab, Tabs, TabList, TabPanel} from 'react-tabs'

class Domain extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            action_names: [],
            intent_names: [],
            entity_names: [],
            templates: [],
            slots: []
        };

        this.update_domain_data = this.update_domain_data.bind(this);
        this.render = this.render.bind(this);
        this.filterTheDomain = this.filterTheDomain.bind(this);
        window.globalBroadcaster.subscribe('trigger_fetch_domain', this.update_domain_data);
        this.update_domain_data();
    }

    componentWillUnmount() {
        window.globalBroadcaster.unsubscribe('trigger_fetch_domain', this.update_domain_data);
    }

    update_domain_data() {

        let endpoint = this.props.dialogueEndpoint + '/api/v2/domain';

        fetch(endpoint, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            method: "GET"
        }).then(
            result => result.json())
            .then(
                (result) => {
                    var intents = [];
                    for (let index = 0; index < result.intents.length; index++) {
                        let intent = result.intents[index];
                        for (var intentKey in intent) {
                            if (intent.hasOwnProperty(intentKey)) {
                                intents.push(intentKey);
                            }
                        }
                    }

                    var templates = [];
                    for (var templateKey in result.templates) {
                        if (result.templates.hasOwnProperty(templateKey)) {
                            templates.push({templateName: templateKey, templateValue: result.templates[templateKey]})
                        }
                    }

                    var slots = [];
                    for (var slotKey in result.slots) {
                        if (result.slots.hasOwnProperty(slotKey)) {
                            slots.push({name: slotKey, data: result.slots[slotKey]});
                        }
                    }

                    this.setState({
                        action_names: result.actions,
                        entity_names: result.entities,
                        intent_names: intents,
                        templates: templates,
                        slots: slots
                    })
                }
            )
            .catch(
                error => console.log('[ERROR]', error));
    }

    filterTheDomain(event) {
        let filterText = event.target.value.toLowerCase();

        this.setState({
            filterText: filterText
        });
    }

    render() {
        let actionsContent = [];
        if (this.state.action_names) {
            for (let itemIndex = 0; itemIndex < this.state.action_names.length; itemIndex++) {
                let item = this.state.action_names[itemIndex];
                if (!this.state.filterText || (item.toLowerCase().indexOf(this.state.filterText) !== -1)) {
                    actionsContent.push(<li key={item} className="domainItem">{item}</li>);
                }
            }
        }

        let entitiesContent = [];
        if (this.state.entity_names) {
            for (let itemIndex = 0; itemIndex < this.state.entity_names.length; itemIndex++) {
                let item = this.state.entity_names[itemIndex];
                if (!this.state.filterText || (item.toLowerCase().indexOf(this.state.filterText) !== -1)) {
                    entitiesContent.push(<li key={item} className="domainItem">{item}</li>);
                }
            }
        }

        let intentsContent = [];
        if (this.state.intent_names) {
            for (let itemIndex = 0; itemIndex < this.state.intent_names.length; itemIndex++) {
                let item = this.state.intent_names[itemIndex];
                if (!this.state.filterText || (item.toLowerCase().indexOf(this.state.filterText) !== -1)) {
                    intentsContent.push(<li key={item} className="domainItem">{item}</li>);
                }
            }
        }

        let templatesContent = [];
        if (this.state.templates) {
            for (var templateIndex = 0; templateIndex < this.state.templates.length; templateIndex++) {
                let template = this.state.templates[templateIndex];

                if (!this.state.filterText || (template.templateName.toLowerCase().indexOf(this.state.filterText) !== -1)) {
                    templatesContent.push(<li key={template.templateName}
                                              className="domainTemplate">{template.templateName}</li>);
                    for (var textIndex = 0; textIndex < template.templateValue.length; textIndex++) {
                        var text = template.templateValue[textIndex];
                        templatesContent.push(<li key={template.templateName + "-" + textIndex.toString()}
                                                  className="domainTemplate message">{text.text}</li>);
                    }
                }
            }
        }

        let variablesContent = [];
        if (this.state.slots) {
            for (let slotIndex = 0; slotIndex < this.state.slots.length; slotIndex++) {
                let slot = this.state.slots[slotIndex];

                if (!this.state.filterText || (slot.name.toLowerCase().indexOf(this.state.filterText) !== -1)) {
                    variablesContent.push(<li key={slot.name} className="domainSlot">{slot.name}</li>);

                    if (slot.data.min_value) {
                        variablesContent.push(<li key={slot.name + "-min_value"}
                                                  className="domainSlot value">{slot.data.min_value} (MIN)</li>);
                    }
                    if (slot.data.max_value) {
                        variablesContent.push(<li key={slot.name + "-max_value"}
                                                  className="domainSlot value">{slot.data.max_value} (MAX)</li>);
                    }

                    if (slot.data.values) {
                        for (var valueIndex = 0; valueIndex < slot.data.values.length; valueIndex++) {
                            var value = slot.data.values[valueIndex];
                            if (value === slot.data.initial_value) {
                                variablesContent.push(<li key={slot.name + "-" + value.toString()}
                                                          className="domainSlot value initial">{value}</li>);
                            } else {
                                variablesContent.push(<li key={slot.name + "-" + value.toString()}
                                                          className="domainSlot value">{value}</li>);
                            }
                        }
                    }
                }
            }
        }

        return (
            <div className="domain">
                <h3>Domain</h3>

                <input type="text" placeholder="Search" onChange={this.filterTheDomain}/>

                <Tabs>
                    <TabList>
                        <Tab>Actions</Tab>
                        <Tab>Entities</Tab>
                        <Tab>Intents</Tab>
                        <Tab>Templates</Tab>
                        <Tab>Variables</Tab>
                    </TabList>

                    <TabPanel>
                        <ul className="domainItems">
                            {actionsContent}
                        </ul>
                    </TabPanel>

                    <TabPanel>
                        <ul className="domainItems">
                            {entitiesContent}
                        </ul>
                    </TabPanel>

                    <TabPanel>
                        <ul className="domainItems">
                            {intentsContent}
                        </ul>
                    </TabPanel>

                    <TabPanel>
                        <ul className="domainTemplates">
                            {templatesContent}
                        </ul>
                    </TabPanel>

                    <TabPanel>
                        <ul className="domainSlots">
                            {variablesContent}
                        </ul>
                    </TabPanel>

                </Tabs>

            </div>
        );
    }
}

export default Domain;
