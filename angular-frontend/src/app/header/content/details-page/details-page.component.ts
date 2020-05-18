import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {DetailedDataModel} from "../search-page/search-results/result/detailed-data-model";
import {BasicDataModel} from "../search-page/search-results/result/basic-data-model";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  detailedData: DetailedDataModel;
  basicData: BasicDataModel;

  constructor(private router: Router) {
    let state = router.getCurrentNavigation().extras.state;
    this.basicData = state.basicData;
    this.detailedData = state.detailedData;
  }

  ngOnInit() {
  }

}
