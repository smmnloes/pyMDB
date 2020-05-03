import {Component, OnInit} from '@angular/core';
import {QueryModel} from "./query-model";
import {ActivatedRoute, Router} from "@angular/router";
import {NgForm} from "@angular/forms";


@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {

  sortCriteria: string[] = ['Title', 'Year', 'Rating'];
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


  constructor(private router: Router, private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(queryParams => {
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
    this.router.navigate(['/search'], {queryParams: JSON.parse(JSON.stringify(this.queryModel))});
  }

}
