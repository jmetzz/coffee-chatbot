/**
 * Very basic means of dispatching messages from event generators to interested subscribers
 */
class GlobalBroadcaster {
    constructor() {
        this.events = {};
    }

    /**
     * Called by event generators to inform subscribers.
     *
     * @param string event: a string identifying the event name
     * @param mix data: message to communicate to subscribers
     */
    dispatch(event, data) {
        if (!this.events[event]) {
            return;
        } // no subscribers
        this.events[event].forEach(subscriber => subscriber.apply(this, data));
    }

    /**
     * Means to subscribe a callback function to a given event.
     * @param string event: a string identifying the event name
     * @param function subscriber: a function to call back when the given event takes place
     */
    subscribe(event, subscriber) {
        if (!this.events[event]) {
            this.events[event] = [];
        } // new event
        this.events[event].push(subscriber);
    }

    unsubscribe(event, subscriber) {
        if (this.events[event]) {
            var index = this.events[event].indexOf(subscriber);
            if (index > -1) {
                this.events[event].splice(index, 1);
            }
        }
    }

    clearSubscriptions() {
        this.events = {};
    }
}

export default GlobalBroadcaster;
