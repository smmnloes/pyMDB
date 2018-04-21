import {Component, OnInit} from '@angular/core';
import {QueryService} from "../../../query.service";
import {Observable} from "rxjs/Observable";
import {ResultModel} from "./result/result-model";

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {

  constructor(private queryService: QueryService) {
  }

  results: Observable<ResultModel[]>;

  ngOnInit() {
    this.results = this.queryService.results$;
  }


}
