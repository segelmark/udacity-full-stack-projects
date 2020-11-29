import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className="Question-holder">
        <div className="flashcard">
          <label>
            <section onClick={() => this.flipVisibility()} className="front" style={{"height": this.state.visibleAnswer ? '0' : '100%'}}>
              <div className="Question-status">
                <div>&nbsp;<img className="category" alt="{category}" src={`${category}.svg`}/></div>
                <div className="difficulty">Difficulty: {difficulty}</div>
                <div>
                  <img src="delete.png" className="delete" alt="Delete {category}" onClick={() => this.props.questionAction('DELETE')}/>
                  &nbsp;
                </div>
              </div>
              <div className="Section-footer">Click to show answer</div>
              <div className="Question-text">{question}</div>
            </section>
            <section className="back"  onClick={() => this.flipVisibility()} style={{"height": this.state.visibleAnswer ? '100%' : '0'}}>
            <div className="Section-footer">Click to hide answer</div>
            <div className="Answer-text">{answer}</div>
            </section>
          </label>
        </div>
      </div>
    );
  }
}

export default Question;
