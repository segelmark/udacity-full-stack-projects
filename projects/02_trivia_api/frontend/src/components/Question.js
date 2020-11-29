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
    const { key, question, answer, category, difficulty } = this.props;
    return (
      <div className="Question-holder">
        <div className="flashcard">
          <label>
            <section onClick={() => this.flipVisibility()} class="front" style={{"height": this.state.visibleAnswer ? '0' : '100%'}}>
              <div className="Question-status">
                <div>&nbsp;<img className="category" src={`${category}.svg`}/></div>
                <div className="difficulty">Difficulty: {difficulty}</div>
                <div>
                  <img src="delete.png" className="delete" onClick={() => this.props.questionAction('DELETE')}/>
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
      // <div className="Question-holder">
      //   <div className="Question">{question}</div>
      //   <div className="Question-status">
      //     <img className="category" src={`${category}.svg`}/>
      //     <div className="difficulty">Difficulty: {difficulty}</div>
      //     <img src="delete.png" className="delete" onClick={() => this.props.questionAction('DELETE')}/>
          
      //   </div>
      //   <div className="show-answer button"
      //       onClick={() => this.flipVisibility()}>
      //       {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
      //     </div>
      //   <div className="answer-holder">
      //     <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
      //   </div>
      // </div>
    );
  }
}

export default Question;
