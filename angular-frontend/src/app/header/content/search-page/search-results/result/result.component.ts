import {Component, Input, OnInit} from '@angular/core';
import {BasicDataModel} from "./basic-data-model";
import {DetailService} from "../../../../../detail.service";
import {DetailedDataModel} from "./detailed-data-model";


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  basicData: BasicDataModel;

  @Input()
  detailedData: DetailedDataModel;

  @Input()
  usedOnDetailsPage: boolean = false;


  constructor(private detailService: DetailService) {
  }

  ngOnInit() {
  }

  getDetails() {
    if (!this.usedOnDetailsPage) {
      this.detailService.getDetails(this.basicData);
    }
  }

}
