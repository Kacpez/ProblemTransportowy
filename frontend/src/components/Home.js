import React, { Component } from 'react'
import Map from './Map.js';

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
          dane: {
            lista_wsporzednych_tras: [],
            macierz_wynikowa: [],
            najlepszy_koszt: 0,
          },
        };
        this.fetchStatus = this.fetchStatus.bind(this);
      }
    
      componentDidMount() {
        this.fetchStatus();
      }
    
      fetchStatus() {
        fetch('http://127.0.0.1:5000/algorytm_optymalizacyjny')
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
         <div className = "Home" > <h1>Algorytm transportowy</h1></div>
            <Map trasy={this.state.dane.lista_wsporzednych_tras} liczba={1} centerList={[this.props.x,this.props.y]}/>
            
<div class="alert alert-success">Najlepszy koszt: {this.state.dane.najlepszy_koszt}</div>
<h2>Macierz wynikowa</h2>
<div className="macierz-wynikowa">
  <table className='content-table2'>
    
    {this.state.dane.macierz_wynikowa.map((wiersz, rowIndex) => {
        if(rowIndex===0){
       return <thead><tr key={rowIndex}>
                 {wiersz.map((element, colIndex) => {
                  if(colIndex===0){
                  return <><td key={colIndex}> </td><td key={colIndex}> Kawiarnia{colIndex+1}</td></>}
                   else{
return <td key={colIndex}>Kawiarnia{colIndex+1} </td>
                   }
        })}
               </tr></thead>}
    })}
<tbody>
      {this.state.dane.macierz_wynikowa.map((wiersz, rowIndex) => (
        
 <tr key={rowIndex}>
  <td>Piekarnia{rowIndex+1}</td>
          {wiersz.map((element, colIndex) => (
            <td key={colIndex}>{element}</td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
  <br></br>
</div>

      </>
        )
    }
}

export default Home;