function Dropdown({ modelo, setModelo }) {
    return (
      <select value={modelo} onChange={(e) => setModelo(e.target.value)}>
        <option value="knn">KNN</option>
        <option value="mlp">MLP</option>
        <option value="dt">Decision Tree</option>
        <option value="rf">Random Forest</option>
        <option value="xgb">XGBoost</option>
      </select>
    );
  }
  
  export default Dropdown;
  