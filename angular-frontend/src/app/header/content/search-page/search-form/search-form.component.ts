import {Component, OnInit} from '@angular/core';
import {QueryModel} from "./query-model";
import {ActivatedRoute, Router} from "@angular/router";
import {Util} from "../../../../util/util";
import {QueryService} from "../../../../services/query.service";


@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {

  sortCriteria: string[] = ['Relevance', 'Title', 'Year', 'Rating'];
  resultsPerPageOptions: number[] = [5, 10, 15, 20, 30, 50];
  queryModel: QueryModel;

  private MAX_CATEGORIES_SELECTABLE: number = 3;
  public genres: string[] = [
    'Action',
    'Adventure',
    'Comedy',
    'Family',
    'Romance',
    'Thriller',
    'Biography',
    'Fantasy',
    'Documentary',
    'Horror',
    'Drama',
    'Sci-Fi',
    'Crime',
    'Animation',
    'War',
    'Mystery',
    'Film-Noir',
    'News',
    'Sport',
    'History',
    'Music',
    'Western',
    'Musical'
  ];


  public genreSelectionPlaceholder: string = 'Select up to ' + this.MAX_CATEGORIES_SELECTABLE + ' genres!';


  constructor(private router: Router, private activatedRoute: ActivatedRoute, private queryService: QueryService) {
  }

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(queryParams => {

        if (!Util.isEmpty(queryParams)) {
          this.queryService.makeQuery(QueryModel.fromQueryParams(queryParams));
        }

        this.queryModel = QueryModel.fromQueryParams(queryParams);
      }
    );
  }

  onSubmit(): void {
    this.queryModel.current_page = 1;
    this.refetch();
  }

  onClickSortBy(): void {
    this.refetch();
  }

  onClickResultsPerPage(): void {
    this.queryModel.current_page = 1;
    this.refetch();
  }

  refetch(): void {
    let queryParams = JSON.parse(JSON.stringify(this.queryModel));
    queryParams.rand = Math.floor(Math.random() * Number.MAX_SAFE_INTEGER);
    this.router.navigate(['/search'], {queryParams: queryParams});
  }

}
