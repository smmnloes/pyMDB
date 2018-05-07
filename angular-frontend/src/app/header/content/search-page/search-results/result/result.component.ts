import {Component, Input, OnInit} from '@angular/core';
import {BasicDataModel} from "./basic-data-model";


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  basicData: BasicDataModel;


  constructor() {
  }

  ngOnInit() {
  }


}
