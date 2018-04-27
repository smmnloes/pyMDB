import {Component, OnInit} from '@angular/core';
import {DetailService} from "../../../detail.service";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  private details: Object;

  constructor(private detailService: DetailService) {
  }

  ngOnInit() {
    this.detailService.currentDetails$.subscribe(details => {
      if (details == null) {
        console.log("NO DETAILS FOUND!");
      } else {
        this.details = details;
        console.log(details);
      }
    })
  }

}
