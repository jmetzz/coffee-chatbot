import React from 'react';

class Button extends React.Component {

    render() {
        return (
            <div>
                <button className="button" disabled={this.props.disabled} onClick={this.props.onClick}>{this.props.label}</button>
            </div>
        );
    }
}

export default Button;
