import {Component, OnInit} from '@angular/core';
import {BasicDataModel} from "./result/basic-data-model";
import {QueryService} from "../../../../services/query.service";

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {

  constructor(private queryService: QueryService) {
  }

  page: BasicDataModel[];

  ngOnInit() {
    this.queryService.basicDataPage$.subscribe(page => {
      this.page = page;
    });
  }


}
