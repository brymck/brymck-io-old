import React, {Component, FormEvent} from 'react';
import Button from '@material/react-button';
import './App.scss';
import TextField, {HelperText, Input} from "@material/react-text-field";
import MaterialIcon from "@material/react-material-icon";
import axios from "axios";

interface AppProps {}

interface AppState {
  value: string
}

class App extends Component<AppProps, AppState> {
  constructor(props: AppProps) {
    super(props);
    this.state = {value: "world"};

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event: FormEvent<HTMLFormElement>) {
    axios.get(`/api/${this.state.value}`)
      .then(response => console.log(response))
      .catch(error => console.log(error));
    event.preventDefault();
  }

  render() {
    return (
      <div className="app">
        <section className="header">
          <h1>BRYMCK.IO</h1>
        </section>
        <form onSubmit={this.handleSubmit}>
          <TextField
            label="Person"
            helperText={<HelperText>Help me!</HelperText>}
            onTrailingIconSelect={() => this.setState({value: ""})}
            trailingIcon={<MaterialIcon role="button" icon="delete" />}
          >
            <Input
              value={this.state.value}
              onChange={(e) => this.setState({value: e.currentTarget.value})}
            />
          </TextField>
          <Button
            raised
            className="button-alternate"
            onClick={() => console.log("clicked!")}
          >
            Click Me!
          </Button>
        </form>
      </div>
    );
  }
}

export default App;
