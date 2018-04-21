import {Component, Input} from '@angular/core';
import {ResultModel} from "./result-model";

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {

  @Input()
  movieData: ResultModel;


}
