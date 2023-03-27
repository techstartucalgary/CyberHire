import React, { useState } from 'react';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import './styles/App.css';

function App() {
  const [displayedForm, setDisplayedForm] = useState('signIn');

  const toggleform = (formName: string) => {
    setDisplayedForm(formName);
  };

  return (
    <>
      
      {displayedForm === 'signIn' ? <SignIn setDisplayedForm={toggleform}/> : <SignUp setDisplayedForm = {toggleform} />}
    </>
  );
}

export default App;