import {Component, OnInit} from '@angular/core';
import {DetailService} from "../detail.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  private currentPage: String = "search";

  constructor(private detailService:DetailService) { }

  ngOnInit() {
    this.detailService.currentDetails$.subscribe(details => this.currentPage = "details");
  }

  public setCurrentPage(page: string) {
    this.currentPage = page;
  }

}
