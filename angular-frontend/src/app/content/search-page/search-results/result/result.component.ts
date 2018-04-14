import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  _movieData: any[];

  constructor() {
  }

  @Input()
  set movieData(movieData: any[]) {
    this.prettify(movieData);
    this._movieData = movieData;
  }

  get movieData() {
    return this._movieData;
  }

  private prettify(movieData: any[]) {
    for (let director of movieData['directors']) {
      director = director + " ";
    }
    console.log(movieData['directors']);

  }

  ngOnInit() {
  }

}
