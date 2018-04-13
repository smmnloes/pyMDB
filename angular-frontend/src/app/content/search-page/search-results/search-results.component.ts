import {Component, OnInit} from '@angular/core';
import {QueryService} from "../../../query.service";
import {Observable} from "rxjs/Observable";

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {

  constructor(private queryService: QueryService) {
  }

  result$: Observable<object[]>;

  results:object[];

  ngOnInit() {
    this.result$ = this.queryService.result$;
    this.result$.subscribe(data => {
      this.results = data;
    })
  }

}
