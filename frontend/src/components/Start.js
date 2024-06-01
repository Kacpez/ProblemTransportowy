import React, { Component } from 'react';
import Map from './Map.js';

class Start extends Component {
    constructor(props) {
      super(props);
      this.state = {
        dane: {
          popyt: [],
          podaz: [],
          macierz_kosztu: [],
        },
      };
      this.fetchStatus = this.fetchStatus.bind(this);
    }
  
    componentDidMount() {
      this.fetchStatus();
    }
  
    fetchStatus() {
      fetch('http://127.0.0.1:5000/')
        .then(response => response.json())
        .then(r => {
          console.log(r);
          this.setState({
            dane: r,
          });
        })
        .catch(error => {
          console.error('Błąd:', error);
        });
    }
  
    render() {
      return (
        <>
          <Map trasy={[]} liczba={0} centerList={[this.props.x,this.props.y]}/>
          <h5>Pomarańczowe markery oznaczają kawiarnie, a niebieskie piekarnie.</h5>
          <h5>Optymalne przydzielanie dostaw z piekarni do kawiarni. W tabeli zostały podane koszty w metrach do pokonania.</h5>
          <h2>Macierz kosztu (Popyt i Podaż)</h2>
          <table className='content-table'>
            <thead>
              <tr>
                <th></th>
                {this.state.dane.podaz.map((_, index) => (
                  <th key={index}>Kawiarnia {index + 1}</th>
                ))}
                <th>Podaż</th>
              </tr>
            </thead>
            <tbody>
              {this.state.dane.macierz_kosztu.map((wiersz, rowIndex) => (
                <tr key={rowIndex}>
                  <td>Piekarnia {rowIndex + 1}</td>
                  {wiersz.map((element, colIndex) => (
                    <td key={colIndex}>{element}</td>
                  ))}
                  <td>{this.state.dane.popyt[rowIndex]}</td>
                </tr>
              ))}
              <tr>
                <td>Popyt</td>
                {this.state.dane.podaz.map((podaz, index) => (
                  <td key={index}>{podaz}</td>
                ))}
                <td>{this.state.dane.popyt.reduce((a, b) => a + b, 0)}</td>
              </tr>
            </tbody>
          </table>
          <br></br>

          {this.state.dane.popyt.length <= 1 || this.state.dane.podaz.length <= 1 ? (
          <div class="alert alert-danger">
           Popyt lub podaż są zbyt małe. Wybierz inne miasto, aby uzyskać poprawne dane.
          </div>
        ):(null)}
        </>
      );
    }
  }
  
  export default Start
  