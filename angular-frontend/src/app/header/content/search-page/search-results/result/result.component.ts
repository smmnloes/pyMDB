import {Component, Input, OnInit} from '@angular/core';
import {BasicDataModel} from "./basic-data-model";
import {DetailService} from "../../../../../services/detail.service";
import {Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";
import {first} from "rxjs/operators";


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  basicData: BasicDataModel;

  @Input()
  activateTitleLink: boolean;

  constructor(private detailService: DetailService, private router: Router, private toastrService: ToastrService) {
  }

  ngOnInit() {
  }

  goToDetailsPage() {
    this.detailService.hasDetails(this.basicData.tid).pipe(first()).subscribe(
      (hasDetails: boolean) => {
        if (hasDetails) {
          this.router.navigate(["/details", this.basicData.tid]);
        } else {
          this.toastrService.warning("No detailed data available");
        }
      },
      error => {
        switch (error.status) {
          case 500:
            this.toastrService.error("Internal Error, try again later")
            break;
          case 404:
            this.toastrService.error(error.error.message);
        }
      }
    );
  }
}
