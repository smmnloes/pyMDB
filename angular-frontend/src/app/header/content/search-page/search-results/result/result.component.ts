import {Component, Input, OnInit} from '@angular/core';
import {BasicDataModel} from "./basic-data-model";
import {DetailService} from "../../../../../detail.service";


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  movieData: BasicDataModel;

  constructor(private detailService: DetailService) {
  }

  ngOnInit() {
  }

  getDetails() {
    this.detailService.getDetails(this.movieData);
  }

}
