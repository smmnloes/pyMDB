import {Component, OnInit} from '@angular/core';
import {Observable} from "rxjs/Observable";
import {BasicDataModel} from "./result/basic-data-model";
import {QueryService} from "../../../../query.service";

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {

  constructor(private queryService: QueryService) {
  }

  results: Observable<BasicDataModel[]>;

  ngOnInit() {
    this.results = this.queryService.basicData$;
  }


}
