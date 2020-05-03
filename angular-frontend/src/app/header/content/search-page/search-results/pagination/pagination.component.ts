import {Component, OnInit} from '@angular/core';
import {QueryService} from "../../../../../services/query.service";
import {ActivatedRoute, Router} from "@angular/router";
import {Util} from "../../../../../util/util";


@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent implements OnInit {
  resultsAvailable = false;
  private currentPage: number;
  private resultCount: number;
  private maxPageCount: number;
  private results_per_page: number;

  constructor(private queryService: QueryService, private router: Router, private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    // if a new result count is published, a new query has been made -> reset current page,
    // calculate new maxPageCount

    this.activatedRoute.queryParams.subscribe(queryParams => {
      if (!Util.isEmpty(queryParams)) {
        this.currentPage = parseInt(queryParams['current_page']);
        this.results_per_page = parseInt(queryParams['results_per_page']);
        this.resultsAvailable = true;
      }
    });

    this.queryService.resultCount$.subscribe(resultCount => {
      this.resultCount = resultCount;
      this.maxPageCount = Math.ceil(<number>resultCount / this.results_per_page);
    })
  }

  onClickPageNr(newPage: number) {
    if (this.currentPage != newPage) {
      this.currentPage = newPage;
      this.loadNewPage();
    }
  }

  onClickNext() {
    if (this.currentPage < this.maxPageCount) {
      this.currentPage++;
      this.loadNewPage();
    }
  }

  onClickPrev() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadNewPage();
    }
  }

  loadNewPage() {
    let params = Object.assign({}, this.activatedRoute.snapshot.queryParams);
    params['current_page'] = this.currentPage;
    this.router.navigate(['/search'], {queryParams: params});
  }

  onClickFirst() {
    if (this.currentPage != 1) {
      this.currentPage = 1;
      this.loadNewPage();
    }
  }

  onClickLast() {
    if (this.currentPage != this.maxPageCount) {
      this.currentPage = this.maxPageCount;
      this.loadNewPage();
    }
  }

  getPages() {
    let pages: number[] = [];
    let minPage = this.currentPage > 5 ? this.currentPage - 5 : 1;
    let maxPage = (this.currentPage > 5 ? this.currentPage + 4 : 10);
    maxPage = maxPage > this.maxPageCount ? this.maxPageCount : maxPage;

    for (let i = minPage; i <= maxPage; i++) {
      pages.push(i);
    }

    return pages;
  }

}
