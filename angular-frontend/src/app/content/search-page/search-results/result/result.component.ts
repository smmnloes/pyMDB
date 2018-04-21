import {Component, Input, OnInit} from '@angular/core';
import {resultModel} from "./resultModel";

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  movieData: resultModel;

  constructor() {
  }

  ngOnInit() {
  }

}
