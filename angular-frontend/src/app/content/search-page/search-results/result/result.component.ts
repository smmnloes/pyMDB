import {Component, Input, OnInit} from '@angular/core';
import {ResultModel} from "./result-model";
import {DetailService} from "../../../../detail.service";

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  movieData: ResultModel;

  constructor(private detailService: DetailService) {
  }

  ngOnInit() {
    this.detailService.currentDetails$.subscribe(details => {
      if (details == null) {
        console.log("ERROR");
      } else {
        console.log(details)
      }

    })
  }

  getDetails() {
    this.detailService.getDetailsByImdbId(this.movieData.tid);
  }

}
